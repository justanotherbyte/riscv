import cocotb
import pytest
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from sim import run


async def load_program(dut, instructions: list[int], start: int = 0x0):
    for i, instr in enumerate(instructions, start=start):
        dut.ins_mem.mem[i].value = instr
        await Timer(1, unit="ns")


async def write_to_data_mem(dut, addr: int, value: int):
    dut.data_mem.mem[(addr >> 2) & 0b111111].value = value
    await Timer(1, unit="ns")


PROGRAM = [
    0xFFC4A303,  # lw x6 -4(x9) (0x1000)
    0x0064A423,  # sw x6, 8(x9) (0x1004)
    0x0062E233,  # or x4, x5, x6 (0x1008)
]


@cocotb.test
async def test_instruction_flow(dut):
    await load_program(dut, PROGRAM, start=0x1)
    await write_to_data_mem(dut, 0x2000, 0xDEADBEEF)

    dut.pc_next.value = 0x4
    dut.reg_file.mem[0x9].value = 0x2004
    dut.reg_file.mem[0x5].value = 0xCAFEBABE

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    assert dut.prog_counter.pc.value == 0x0
    assert dut.reg_file.A1.value == 0x0
    assert dut.reg_file.RD1.value == 0x0

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.reg_file.RD1.value == 0x2004
    assert dut.alu_result.value == 0x2000

    assert dut.read_data.value == 0xDEADBEEF

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.reg_file.mem[0x6].value == 0xDEADBEEF

    dut.reg_file_WE.value = 0  # the sw instruction does not write to the register file.
    dut.data_mem_WE.value = 1  # the sw instruction writes to data memory.
    dut.imm_src.value = 1  # s-type immediate

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert (
        dut.data_mem.mem[(0x200C >> 2) & 0b111111].value == 0xDEADBEEF
    )  # 0x200C comes from 0x2004 + 8

    dut.result_src.value = 0
    dut.alu_src.value = 0
    dut.data_mem_WE.value = 0
    dut.reg_file_WE.value = 1
    dut.alu_ctrl.value = 0b011

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.reg_file.mem[0x4].value == 0xCAFEBABE | 0xDEADBEEF


@pytest.mark.parametrize("testcase", ["test_instruction_flow"])
def test_data_path(testcase: str):
    run(
        "data_path",
        [
            "data_path.sv",
            "ins_mem.sv",
            "reg_file.sv",
            "pc.sv",
            "data_mem.sv",
            "alu.sv",
            "extend.sv",
        ],
        "test_data_path",
        testcase,
    )

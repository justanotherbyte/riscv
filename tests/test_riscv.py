import cocotb
import pytest
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from sim import run


@cocotb.test
async def test_lw_instruction(dut):
    instruction = 0xFFC4A303  # lw x6 -4(x9)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.pc_next.value = instruction

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.pc.value == instruction


async def load_program(dut, instructions: list[int], start: int = 0x0):
    for i, instr in enumerate(instructions, start=start):
        dut.ins_mem.mem[i].value = instr
        await Timer(1, unit="ns")


async def write_to_data_mem(dut, addr: int, value: int):
    dut.data_mem.mem[(addr >> 2) & 0b111111].value = value
    await Timer(1, unit="ns")


@cocotb.test
async def test_instruction_flow(dut):
    await load_program(dut, [0xFFC4A303], start=0x1)
    await write_to_data_mem(dut, 0x2000, 0xDEADBEEF)
    dut.pc_next.value = 0x4
    dut.reg_file.mem[0x9].value = 0x2004

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    assert dut.prog_counter.pc.value == 0x0
    assert dut.reg_file.A1.value == 0x0
    assert dut.reg_file.RD1.value == 0x0

    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.reg_file.RD1.value == 0x2004
    assert dut.alu_result.value == 0x2000

    assert dut.read_data.value == 0xDEADBEEF

    dut.reg_file.A2.value = 0x6
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    assert dut.reg_file.RD2.value == 0xDEADBEEF


@pytest.mark.parametrize("testcase", ["test_lw_instruction", "test_instruction_flow"])
def test_riscv(testcase):
    run(
        "riscv",
        [
            "riscv.sv",
            "ins_mem.sv",
            "reg_file.sv",
            "pc.sv",
            "data_mem.sv",
            "alu.sv",
            "extend.sv",
        ],
        "test_riscv",
        testcase,
    )

import cocotb
from cocotb.triggers import Timer
from sim import run


def bits(instr: int, msb: int, lsb: int) -> int:
    return (instr >> lsb) & ((1 << (msb - lsb + 1)) - 1)


@cocotb.test
async def test_extend_(dut):
    instr = 0x0064A423

    dut.imm.value = bits(instr, 31, 7)
    dut.imm_src.value = 1
    await Timer(1, unit="ns")

    assert dut.imm_ext.value == (bits(instr, 31, 25) << 5) | bits(instr, 11, 7)

    dut.imm.value = bits(instr, 31, 7)
    dut.imm_src.value = 0
    await Timer(1, unit="ns")

    assert dut.imm_ext.value == bits(instr, 31, 20)


def test_extend():
    run("extend", ["extend.sv"], "test_extend")

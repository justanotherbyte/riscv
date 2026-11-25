import random

import cocotb
from cocotb.triggers import Timer
from sim import run


@cocotb.test
async def test_extend_(dut):
    dut.imm.value = 1
    await Timer(1, unit="ns")

    assert dut.imm_ext.value == 1

    num = -random.randint(1, 250)

    dut.imm.value = num
    await Timer(1, unit="ns")

    assert dut.imm_ext.value == num


def test_extend():
    run("extend", ["extend.sv"], "test_extend")

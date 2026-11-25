import random

import cocotb
from cocotb.triggers import Timer
from sim import run


@cocotb.test
async def test_alu_addition(dut):
    src_a = random.randint(1, 100)
    src_b = random.randint(1, 100)

    dut.ctrl.value = 0
    dut.src_a.value = src_a
    dut.src_b.value = src_b

    await Timer(1, unit="ns")

    assert dut.result.value == src_a + src_b


def test_alu():
    run("alu", ["alu.sv"], "test_alu")

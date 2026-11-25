import cocotb
from cocotb.triggers import Timer
from sim import run


@cocotb.test
async def test_get_value(dut):
  await Timer(1, unit="ns")
  # print(dut.mem[0].value)
  assert True


def test_ins_mem():
    run("ins_mem", ["ins_mem.sv"], "test_ins_mem")

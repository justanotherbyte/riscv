import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from sim import run


async def write_to_address(dut, address: int, value: int):
  dut.WE3.value = 1
  dut.WD3.value = value
  dut.A3.value = address
  await RisingEdge(dut.clk)
  await Timer(1, unit="ns")
  dut.WE3.value = 0

@cocotb.test
async def test_read_write(dut):
  cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

  await write_to_address(dut, 0x7, 0x8)
  await write_to_address(dut, 0x8, 0xA)
  await write_to_address(dut, 0x0, 0xF)

  dut.A1.value = 0x7
  dut.A2.value = 0x8
  await Timer(1, unit="ns")

  assert dut.RD1.value == 0x8
  assert dut.RD2.value == 0xA

  dut.A1.value = 0x0
  await Timer(1, unit="ns")

  assert dut.RD1.value == 0x0



def test_reg_file():
    run("reg_file", ["reg_file.sv"], "test_reg_file")

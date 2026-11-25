import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from sim import run


async def write_to_address(dut, address: int, value: int):
    dut.WE.value = 1
    dut.A.value = address
    dut.WD.value = value
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")

    dut.WE.value = 0


async def read_from_address(dut, address: int) -> int:
    dut.WE.value = 0
    dut.A.value = address
    await Timer(1, unit="ns")

    return dut.RD.value


@cocotb.test
async def test_read_write(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    await write_to_address(dut, 0x7, 0x8)
    await write_to_address(dut, 0x8, 0xA)
    await write_to_address(dut, 0x0, 0xF)

    assert await read_from_address(dut, 0x0) == 0xF
    assert await read_from_address(dut, 0x7) == 0x8
    assert await read_from_address(dut, 0x8) == 0xA


def test_data_mem():
    run("data_mem", ["data_mem.sv"], "test_data_mem")


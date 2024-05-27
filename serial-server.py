import serial
from openpyxl import Workbook

class Position:
    def __init__(self, column='A', row=1):
        self.row = row
        self.column = column

    def __repr__(self):
        return self.to_str()

    def increase_column(self, n):
        self.column = chr(ord(self.column) + n)

    def decrease_column(self, n):
        self.column = chr(ord(self.column) - n)

    def increase_row(self, n):
        self.row += n

    def decrease_row(self, n):
        self.row -= n
    def to_str(self):
        return self.column + str(self.row)

    def copy(self):
        return Position(self.column,self.row)


print("ENTER Serial Port:")
print("Example: (COM7) without parenthesis")
serial_port = input()

arduino_serial = serial.Serial(baudrate=115200, port=serial_port)



print("ENTER FILE NAME: ")
filename = input()

if filename == "":
    print("DEFAULT FILE NAME: test.xlsx")
    filename = 'test.xlsx'

print("ENTER SAMPLE SIZE: ")
sample_size = input()

if sample_size == "":
    print("DEFAULT SAMPLE SIZE: 5")
    sample_size = 5
else:
    sample_size = int(sample_size)

workbook = Workbook()
worksheet = workbook.worksheets[0]

worksheet['A1'] = 'MQ2'
worksheet['B1'] = 'MQ5'
worksheet['C1'] = 'MQ7'
worksheet['D1'] = 'Temp'
worksheet['E1'] = 'Humidity'
worksheet['F1'] = 'PM 1.0'
worksheet['G1'] = 'PM 2.5'
worksheet['H1'] = 'PM 10.0'

while True:
    data = arduino_serial.read(1)
    if data.decode() == '\n':
        break
buffer = ""

position = Position(column='A',row=2)

current = 0
while True:
    if current == sample_size:
        break
    data = arduino_serial.read(1).decode()
    if data == '\r':
        continue
    if data == '\n':
        print(buffer)
        buffer = buffer.split(',')
        line_position = position.copy()
        for reading in buffer:
            print(reading)
            print(line_position.to_str())
            worksheet[line_position.to_str()] = reading
            line_position.increase_column(1)
        position.increase_row(1)
        buffer = ""
        current += 1
        continue
    buffer += data
workbook.save(filename)
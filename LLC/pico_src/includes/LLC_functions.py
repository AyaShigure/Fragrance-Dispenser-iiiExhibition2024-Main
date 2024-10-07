from machine import Pin, PWM, ADC
import time

# This function set is for direct hardware control, the most basic functions

def pin_init():
    for i in range(26):
        pin = Pin(i, Pin.OUT)
        pin.off() 

def beep(count):
    buzzer = Pin(0, Pin.OUT)
    for i in range(count):
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)
        
def boot():
    pin_init()
    beep(6)

# Controller class
class tb6600:
    def __init__(self, step_pin, direction_pin, enable_pin):
        self.step = Pin(step_pin, Pin.OUT)   
        self.direction = Pin(direction_pin, Pin.OUT) 
        self.enable = Pin(enable_pin, Pin.OUT) 

        self.enable.off()  
        self.direction.off() 

    def enable_motor(self):
        self.enable.on()

    def disable_motor(self):
        self.enable.off()

    def set_direction(self, direction):
        self.direction.value(direction)

    def pulse(self, delay_us=1000):
        self.step.on()
        time.sleep_us(delay_us)
        self.step.off()
        time.sleep_us(delay_us)

    def rotate(self, steps, direction):
        division_steps = int(steps/len(self.delay_us_table))
        self.direction.value(direction)
        for i in range(len(self.delay_us_table)):
            delay = self.delay_us_table[i]
            for _ in range(division_steps):
                self.pulse(delay_us=delay)

    def rotate_with_ramp(self, steps, direction, min_delay_us=1000, max_delay_us=5000, ramp_steps=50):
        self.set_direction(direction)
        self.enable_motor()
        delay_table = []

        for i in range(ramp_steps):
            delay = max_delay_us - (max_delay_us - min_delay_us) * (i / ramp_steps)
            delay_table.append(int(delay))

        if steps > 2 * ramp_steps:
            delay_table.extend([min_delay_us] * (steps - 2 * ramp_steps))

        for i in range(ramp_steps):
            delay = min_delay_us + (max_delay_us - min_delay_us) * (i / ramp_steps)
            delay_table.append(int(delay))

        for delay in delay_table:
            self.pulse(delay)

        self.disable_motor()


# pin 18 ,25
class Servo:
    def __init__(self, pin, freq=50, min_duty=1000, max_duty=9000, initial_angel=90):
        """初始化伺服电机

        参数:
        pin (int): 伺服电机控制信号连接的 GPIO 引脚编号
        freq (int): PWM 信号频率（默认为 50Hz）
        min_duty (int): 最小占空比（默认为 1000）
        max_duty (int): 最大占空比（默认为 9000）
        name (str): 伺服电机的名称
        """
        self.pin = Pin(pin)
        self.pwm = PWM(self.pin)
        self.pwm.freq(freq)
        self.min_duty = min_duty
        self.max_duty = max_duty
        
        # 初始化位置到中间
        self.set_angle(initial_angel)

    def set_angle(self, angle):
        """设置伺服电机的角度

        参数:
        angle (float): 目标角度（0 到 180）
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180

        # 将角度转换为对应的占空比
        duty = self.angle_to_duty(angle)
        self.pwm.duty_u16(duty)

    def angle_to_duty(self, angle):
        """将角度转换为 PWM 的占空比

        参数:
        angle (float): 角度（0 到 180）
        
        返回:
        int: 对应的 PWM 占空比
        """
        return int(self.min_duty + (self.max_duty - self.min_duty) * (angle / 180))

    def deinit(self):
        """停用 PWM 信号，释放引脚资源"""
        self.pwm.deinit()

class ADCReader:
    def __init__(self, pin, vref=3.3, name="ADC Reader"):
        """初始化 ADC 读取器

        参数:
        pin (int): ADC 连接的 GPIO 引脚编号（A0, A1, A2 等）
        vref (float): 参考电压（默认 3.3V）
        name (str): ADC 的名称
        """
        self.adc = ADC(Pin(pin))  # 初始化 ADC 引脚
        self.vref = vref  # 参考电压
        self.name = name  # ADC 名称

    def read_raw(self):
        """读取原始 ADC 值

        返回:
        int: 原始 ADC 值（0-65535）
        """
        return self.adc.read_u16()

    def read_voltage(self):
        """读取转换后的电压值

        返回:
        float: 转换后的电压值（以伏为单位）
        """
        raw_value = self.read_raw()
        voltage = raw_value * (self.vref / 65535)  # 计算电压
        return voltage

    def print_status(self):
        """打印当前 ADC 的状态和电压值"""
        voltage = self.read_voltage()
        print(f"ADC '{self.name}' Voltage: {voltage:.2f}V")


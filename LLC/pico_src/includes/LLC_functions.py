from machine import Pin, PWM, ADC
import time

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





# Controller class
class tb6600:
    def __init__(self, step_pin, direction_pin, enable_pin):
        self.step = Pin(step_pin, Pin.OUT)   
        self.direction = Pin(direction_pin, Pin.OUT) 
        self.enable = Pin(enable_pin, Pin.OUT) 

        self.enable.off()  
        self.direction.off() 
        self.delay_us_table = [1200, 1150, 1100, 1050, 1000, 950, 900, 850, 800, 750, 700, 650, 600, 550, 500]
        # self.delay_us_table = [1000, 900, 800, 700, 600 , 500, 400]
        # for i,item in enumerate(self.delay_us_table):
        #     self.delay_us_table[i] = int(item/4)

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

    def tick_tock(self,steps):
        for _ in range(steps):
            self.pulse()
            # time.sleep(0.01)

    def lock_pose(self):
        self.step.on()
        time.sleep(0.01)
        self.step.off()
        time.sleep(0.01)

    def rotate(self, steps, direction):
        division_steps = int(steps/len(self.delay_us_table))
        self.direction.value(direction)
        for i in range(len(self.delay_us_table)):
            delay = self.delay_us_table[i]
            for _ in range(division_steps):
                self.pulse(delay_us=delay)


    # def pulse(self, delay_us=1000):
    #     self.step.on()
    #     time.sleep_us(delay_us)
    #     self.step.off()
    #     time.sleep_us(delay_us)

    # def rotate_with_ramp(self, steps, direction, min_delay_us=1000, max_delay_us=5000, ramp_steps=50):
    #     self.set_direction(direction)
    #     self.enable_motor()
    #     run_cycle = 50
    #     # 加速阶段
    #     for i in range(ramp_steps):
    #         delay = max_delay_us - (max_delay_us - min_delay_us) * (i / ramp_steps)
    #         self.pulse(int(delay))

    #     # 恒速阶段
    #     for _ in range(steps - 2 * ramp_steps):
    #         self.pulse(min_delay_us)

    #     # 减速阶段
    #     for i in range(ramp_steps):
    #         delay = min_delay_us + (max_delay_us - min_delay_us) * (i / ramp_steps)
    #         self.pulse(int(delay))

    #     self.disable_motor()






class LimitSwitch:
    def __init__(self, pin, active_low=True, pull_up=True, name="Limit Switch"):
        """初始化限位开关

        参数:
        pin (int): 限位开关连接的 GPIO 引脚编号
        active_low (bool): 是否使用低电平作为触发状态（默认 True）
        pull_up (bool): 是否使用内部上拉电阻（默认 True）
        name (str): 限位开关的名称
        """
        self.pin = Pin(pin, Pin.IN, Pin.PULL_UP if pull_up else None)
        self.active_low = active_low  # 是否低电平触发
        self.name = name  # 限位开关的名称

    def is_triggered(self):
        """检查限位开关是否被触发

        返回:
        bool: 如果限位开关被触发，返回 True，否则返回 False
        """
        # 根据电平状态和是否低电平触发来判断是否被触发
        if self.active_low:
            return not self.pin.value()  # 低电平为被触发状态
        else:
            return self.pin.value()  # 高电平为被触发状态

    def print_status(self):
        """打印限位开关的状态"""
        status = "Triggered" if self.is_triggered() else "Not Triggered"
        print(f"Limit Switch '{self.name}': {status}")

class Servo:
    def __init__(self, pin, freq=50, min_duty=1000, max_duty=9000, name="Servo Motor"):
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
        self.name = name
        
        # 初始化位置到中间
        self.set_angle(90)

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


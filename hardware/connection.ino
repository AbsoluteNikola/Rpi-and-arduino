#include <TroykaMQ.h>
#include <DHT.h>
#include <Wire.h>
#include <TMP36.h>
#include <TroykaIMU.h>
#include <MPU6050.h>

DHT dht(7, DHT11);
Barometer barometer;
MQ135 mq135(A0);
MQ7 mq7(A1);
MPU6050 mpu;


void send_buf(char *buf, int len, int stopbyte=1) {
  Serial.write(buf, len);
}

void send_msg(String msg) {
  int ack = 0, r = 0;
  while(!ack)
  {
    unsigned long long start = millis();
  // resend msg if it was breaked
    send_buf(msg.c_str(), msg.length() + 1);
    unsigned long hash = hash_msg(msg);
    send_buf((char*)&hash, sizeof(hash));
    while(!Serial.available() && millis() - start < 100);
    if(Serial.available())
    {
      r = Serial.read();
      if(r == 'A')
        ack = 1;
    }
  }
}

unsigned long hash_msg(String msg) {
// 32 bit hash
  unsigned long hash = 0, num = 23;
  unsigned long mod = 1000000007;
  hash = msg[0] * num;
  for(int i = 1; i < msg.length(); i++) {
    num = ((unsigned long long)num * 23) % mod;
    hash = ((unsigned long long)hash + (unsigned long long)num * msg[i]) % mod;
  }
  return hash;
}

void setup()
{
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  Serial.begin(9600);
  barometer.begin();
  dht.begin();
  digitalWrite(9, 1);
  delay(40000);
  mq7.calibrate();
  mq135.calibrate();
  digitalWrite(9, 0);
  digitalWrite(10, 1);
  mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G);
  mpu.calibrateGyro();

}

void loop()
{
  //send_msg("start loop");
  Vector rawGyro = mpu.readRawGyro();

  float v_sys = analogRead(A4)*16.395/1024;
  float v_heat = analogRead(A3)*15.44/1024;

  int p_sys = 100*v_sys/16.8;
  int p_heat = 100*v_heat/12.6;

  if(p_sys > 100){
    p_sys = 100;
    }
  if(p_heat > 100){
    p_heat = 100;
    }
  String p = "pressure:" + String(barometer.readPressureMillibars());
  String t1 = "temperature_1:" + String(barometer.readTemperatureC());
  String t2 = "temperature_2:" + String(dht.readTemperature());
  String h = "humidity:" + String(dht.readHumidity());
  String co2 = "CO2:" + String(mq135.readCO2());
  String co = "CO:" + String(mq7.readCarbonMonoxide());
  String v_s = "voltage_system:" + String(p_sys);
  String v_h = "voltage_heater:" + String(p_heat);
  String g_x = "gyro_x:" + String(rawGyro.XAxis);
  String g_y = "gyro_y:" + String(rawGyro.YAxis);
  String g_z = "gyro_z:" + String(rawGyro.ZAxis);

  send_msg(p);
  send_msg(h);
  send_msg(co2);
  send_msg(co);
  send_msg(t1);
  send_msg(t2);
  send_msg(v_s);
  send_msg(v_h);
  send_msg(g_x);
  send_msg(g_y);
  send_msg(g_z);

  delay(1000);
}

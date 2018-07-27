
#include <Wire.h>
#include <TMP36.h>
#include <TroykaIMU.h>


TMP36 Temp_1(A0, 5.0);
Barometer barometer;

void setup()
{ 
  Serial.begin(115200);
  barometer.begin();
}

void send_buf(char *buf, int len, int stopbyte=1) {
  Serial.write(buf, len);
}

void send_msg(String msg) {
  int ack = 0, r = 0;
  while(!ack)
  {
  // resend msg if it was breaked
    send_buf(msg.c_str(), msg.length() + 1);
    unsigned long hash = hash_msg(msg);
    send_buf((char*)&hash, sizeof(hash));
    while(!Serial.available());
    r = Serial.read();
    if(r == 'A')
      ack = 1;
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

void loop()
{
  String pressure = "pressure:" + String(barometer.readPressureMillibars());
  String temperature = "temperature1:" + String(barometer.readTemperatureC());
  String celsius = "temperature2:" + String(Temp_1.getTempC());

  send_msg(pressure);
  send_msg(temperature);
  send_msg(celsius);
  //!!!!!!!!!!!!!!!!!!!!!!!!!
  delay(100);
}

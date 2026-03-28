#include <Adafruit_NeoPixel.h>

#define LED_PIN    5
#define LED_COUNT 100

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  strip.show();
  Serial.begin(115200);
  Serial.setTimeout(50); // Fast timeout for responsive updates
}

void loop() {
  if (Serial.available() > 0) {
    char header = Serial.read();

    if (header == 'X') {
      uint8_t buffer[300];
      // Read exactly 300 bytes (100 LEDs * 3 colors)
      size_t n = Serial.readBytes(buffer, 300);
      
      if (n == 300) {
        for (int i = 0; i < LED_COUNT; i++) {
          // Data is already in G-R-B order from Python
          strip.setPixelColor(i, buffer[i*3], buffer[i*3+1], buffer[i*3+2]);
        }
        strip.show();
      }
    } 
    else if (header == 'T') {
      rainbow(5);
      while(Serial.available() > 0) Serial.read(); // Clear buffer after rainbow
    }
  }
}

void rainbow(int wait) {
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    strip.rainbow(firstPixelHue);
    strip.show();
    delay(wait);
    // If a new command 'X' arrives, stop the rainbow immediately
    if (Serial.available() > 0 && Serial.peek() == 'X') return;
  }
}
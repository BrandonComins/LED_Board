#include <Adafruit_NeoPixel.h>

#define LED_PIN    5
#define LED_COUNT 100

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();
  
  // --- STARTUP CHECK --- 
  // If this doesn't light up when you run Python, the COM port is wrong.
  strip.setPixelColor(0, 0, 255, 0); // Bright Green
  strip.show();
  delay(1000);
  strip.clear();
  strip.show();

  Serial.begin(115200);
  Serial.setTimeout(10); 
}

void loop() {
  if (Serial.available() > 0) {
    // Check if it's a Test signal first
    if (Serial.peek() == 'T' || Serial.peek() == 't') {
      Serial.read(); // Clear the 'T'
      rainbow(5);
      return;
    }

    // Use parseInt to grab the 4 numbers directly
    int idx = Serial.parseInt();
    int r   = Serial.parseInt();
    int g   = Serial.parseInt();
    int b   = Serial.parseInt();

    // Check for the newline to clear the buffer
    if (Serial.read() == '\n' || Serial.available() > 0) {
      // ONLY update if the index is valid
      if (idx >= 0 && idx < LED_COUNT) {
        strip.setPixelColor(idx, r, g, b);
        strip.show();
      }
    }
  }
}

// Simple but robust parser
bool parse(String s, int* arr) {
  int count = 0;
  int lastIdx = 0;
  for (int i = 0; i < s.length(); i++) {
    if (s[i] == ' ') {
      arr[count++] = s.substring(lastIdx, i).toInt();
      lastIdx = i + 1;
      if (count >= 3) break;
    }
  }
  arr[count++] = s.substring(lastIdx).toInt();
  return (count == 4); // Returns true only if we found 4 numbers
}

void rainbow(int wait) {
  for(long firstPixelHue = 0; firstPixelHue < 5*65536; firstPixelHue += 256) {
    strip.rainbow(firstPixelHue);
    strip.show();
    delay(wait);
    if (Serial.available() > 0) return; // Stop if user clicks a button
  }
}
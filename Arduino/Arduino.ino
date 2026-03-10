#include <Adafruit_NeoPixel.h>

constexpr int led_pin = 5;
constexpr int led_count = 100;
const bool debug = false;

int colorArr[4] = {-1, -1, -1, -1}; // LED #, R, G, B,
Adafruit_NeoPixel strip(led_count, led_pin, NEO_GRB + NEO_KHZ800);

void test_LEDS() {
  rainbow(5);
  delay(10);
  strip.clear();
}

void setup(){
  strip.begin();           // Initialize NeoPixel object
  strip.setBrightness(255); // Set BRIGHTNESS to about 4% (max = 255)
  strip.show();            // Initialize all pixels to 'off'
  Serial.begin(9600);
}

void loop() {
  if (!debug && Serial.available() > 0) {
    // Read until a newline for faster response
    String input = Serial.readStringUntil('\n'); 
    split(input, ' ');

    strip.setPixelColor(colorArr[0], colorArr[1], colorArr[2], colorArr[3]);
    strip.show();
  } else if (debug) {
    test_LEDS();
  }
}

/**
 * Splits a delimited string into integers and stores them in a global array.
 * * This function iterates through a string, parses segments separated by a 
 * specific character (e.g., a comma), converts those segments to integers, 
 * and populates the global 'colorArr' array with the results.
 *
 * @param str   The input String containing delimited numeric values.
 * @param split The delimiter character used to separate values (e.g., ',' or ':').
 * * @note This function assumes 'colorArr' is large enough to hold all parsed values.
 * @warning Relies on the global variable 'colorArr'. Be careful of buffer overflows
 * if the input string contains more segments than the array size.
 */
void split(String str, const char split){
  int index = 0;
  Serial.println(str);
  String temp = "";
  
  for(int i = 0; i <= str.length(); ++i){
    if(str[i] == split || str[i] == '\0'){
      	colorArr[index] = temp.toInt();
      	++index;
      	temp = "";	
    }else{
      temp += str[i];
    }
  }
}

void rainbow(int wait) {
  for(long firstPixelHue = 0; firstPixelHue < 256*100; firstPixelHue += 256) {
    strip.rainbow(firstPixelHue);
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}
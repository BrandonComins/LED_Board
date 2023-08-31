#include <Adafruit_NeoPixel.h>

#define LED_PIN 5
#define LED_COUNT 100

int colorArr[4] = {-1, -1, -1, -1};
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);


void setup(){
  strip.begin();           // Initialize NeoPixel object
  strip.setBrightness(255); // Set BRIGHTNESS to about 4% (max = 255)
  strip.show();            // Initialize all pixels to 'off'
  Serial.begin(9600);
}

void loop()
{
  if(Serial.available()){
    String input = Serial.readString();
   	split(input, ' ');

  	strip.setPixelColor(
      colorArr[0],
      colorArr[1],
      colorArr[2],
      colorArr[3]
    );
    strip.show();

  }
  //rainbow(5);
  //delay(10);
  //strip.clear();
}

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
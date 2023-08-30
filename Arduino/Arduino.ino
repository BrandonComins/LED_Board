void setup(){
	Serial.begin(9600);
}

void loop(){
  if(Serial.available()){
    String input = Serial.readString();
    static int * valuesArr = split(input, ' ');
      
    int position = valuesArr[0];
    int red = valuesArr[1];
    int green = valuesArr[2];
    int blue = valuesArr[3];

    Serial.println(position);
    Serial.println(red);
    Serial.println(blue);
    Serial.println(green);
  }
}

static int * split(String str, const char split){
  int index = 0;
  Serial.println(str);
  static int tempArr[4] = {-1, -1, -1, -1};
  String temp = "";
  
  for(int i = 0; i <= str.length(); ++i){
    if(str[i] == split || str[i] == '\0'){
      tempArr[index] = temp.toInt();
      ++index;
      temp = "";	
    }else{
      temp += str[i];
    }
  }
  return tempArr;
}


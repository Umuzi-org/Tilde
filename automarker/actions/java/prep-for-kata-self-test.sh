cd $DESTINATION_PATH
 

cp $(find app/src/main/java -name "*.java") .
rm -rf app
rm -rf .gitattributes
rm -rf .gitignore
rm -rf .gradle
rm -rf gradle
rm -rf gradlew
rm -rf gradlew.bat
rm -rf settings.gradle
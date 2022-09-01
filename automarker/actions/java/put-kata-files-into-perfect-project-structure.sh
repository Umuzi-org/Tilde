cd $DESTINATION_PATH

cp -r  $PERFECT_PROJECT_PATH/* .

# note: the directory structure could be slightly different from the perfect project structure! eg 
# task1_java/app/src/main/java/task1/Task1.java would change to this:
# task1_java/app/src/main/java/Task1.java

rm -rf  app/src/main/java/
mkdir  app/src/main/java/ 

ls | grep ".java"

for x in *.java; do 
    mv $x app/src/main/java/
done

# Automarker 3 

This project is an improvement on the last version of the automarker. It is designed to overcome certain shortcomings in previous versions.

## How to run 


For now this is just a poc. So it only works for one project

```
cd src 
python marker.py 
```


## Shortcomings to overcome 

The previous version has the following problems:

1. unDRY project configuration 

If we write configuration for a single project in multiple languages, then the various test cases need to be rewritten in multiple languages. There is no way for data to be shared.

2. central configuration file:

The code and the config are seperate. The configuration file is unweildly and so people keep putting things in random places instead of grouping configs sensibly. Config should be colocated with the code

3. Only one level of failure 

We should allow multiple levels. Eg: if the learner's code doesn't run at all (meaning, they didn't run it at all) then we would want to give them a bad review. On the other hand if there is just a little bug we should not be as harsh. 

4. Rigid configuration 

It would be useful to be able to tweak the steps in different marker pipelines. Right now the only way to do that is to create whole new markers.

5. Testing frameworks do weird things between different languages

Logs and errors get swallowed in different ways. It's hard to be consistent about gathering info and sharing it with the user.

6. Error text is not user-friendly

Due to the weird things that happen between languages, it is hard to give learners good quality feedback. 

7. No visibility of test runs

If this was a CI/CD thing then we would be able to see what happened over time. What was run, when it was run, what step happened when... Currently the automarker is pretty opaque.

8. Multi-part projects need DRY tests

Currently, if there is a multi-part project we need to explicitly copy tests from one perfect project to the next. We should be able to extend things somehow.

9. Now way to track performance of an automarker config over time. We can see reviews that were left, but we can't see when a user needed to step in and stop the process. 

10. Self-test is a pain in the bum. It would be nice to be able to run a self-test for everything with a single command
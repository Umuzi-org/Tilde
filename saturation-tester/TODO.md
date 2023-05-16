
# Who am i

- [ ] attempt to store whoami in cookie or something so we don't need to fetch it on every page load
- [ ] Reduce returned payload from whoami

# retires

- [ ]  build retries into server side prop api calls 

# image pull policy

- [ ] see how this effects things

# Automarker 

- [ ] what happens if I decrease number of automarkers in play
- [ ] set max ram etc 


locust -f src/locustfile_backend_apis_for_mini_frontend.py --headless --html reports/backend_slow_ramp_up.html -u 1000 --run-time 30m -r 1 --stop-timeout 10s



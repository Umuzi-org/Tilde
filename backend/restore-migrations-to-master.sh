#!/bin/sh

rm -rf core/migrations
rm -rf attendance/migrations
rm -rf curriculum_tracking/migrations
rm -rf git_real/migrations
rm -rf social_auth/migrations
rm -rf config/migrations
rm -rf activity_log/migrations
rm -rf automarker/migrations
rm -rf zero_marginal_cost_challenges/migrations
rm -rf project_review_coordination/migrations
rm -rf session_scheduling/migrations
rm -rf selection_bootcamps/migrations
rm -rf coderbyte_tests/migrations
rm -rf project_review_pricing/migrations


git checkout master -- core/migrations
git checkout master -- attendance/migrations
git checkout master -- curriculum_tracking/migrations
git checkout master -- git_real/migrations
git checkout master -- social_auth/migrations
git checkout master -- config/migrations
git checkout master -- activity_log/migrations
git checkout master -- automarker/migrations
git checkout master -- zero_marginal_cost_challenges/migrations
git checkout master -- project_review_coordination/migrations
git checkout master -- session_scheduling/migrations
git checkout master -- selection_bootcamps/migrations
git checkout master -- coderbyte_tests/migrations
git checkout master -- project_review_pricing/migrations





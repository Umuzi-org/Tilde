import { _toCamel, fromSnakeToCamel } from "./apiHelpers";

test("_toCamel should format all snake case variables to camel case", () => {
  expect(_toCamel("object_1_summary")).toBe("object1Summary");
  expect(_toCamel("object_1_Id")).toBe("object1Id");
});

test("fromSnakeToCamel should format all camel case properties of an object to snake case", () => {
  const entryLog = {
    id: 137,
    timestamp: "2022-10-12T08:31:32.819526Z",
    event_type: 3,
    actor_user: 18,
    effected_user: 18,
    actorUser_email: "faith.mofokeng@umuzi.org",
    effected_user_email: "faith.mofokeng@umuzi.org",
    object_1_content_type_name: "curriculum_tracking | topic progress",
    object_1_id: 16,
    object_2_content_type_name: null,
    object_2_id: null,
  };
  const formattedEntryLog = {
    id: 137,
    timestamp: "2022-10-12T08:31:32.819526Z",
    eventType: 3,
    actorUser: 18,
    effectedUser: 18,
    actorUserEmail: "faith.mofokeng@umuzi.org",
    effectedUserEmail: "faith.mofokeng@umuzi.org",
    object1ContentTypeName: "curriculum_tracking | topic progress",
    object1Id: 16,
    object2ContentTypeName: null,
    object2Id: null,
  };
  expect(fromSnakeToCamel(entryLog)).toEqual(formattedEntryLog);
});

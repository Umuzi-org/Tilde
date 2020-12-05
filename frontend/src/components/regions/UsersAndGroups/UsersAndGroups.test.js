import {cleanAndFilterUserGroups} from "."

const userGroups = {
    "1":{
        "id":1,"name":"demo group 1 AAA","active":true,"members":[{"userId":1,"userEmail":"sheena.oconnell@umuzi.org","permissionStudent":true,"permissionView":false,"permissionManage":false}]},
    2: {
        "id":2, name: "demo group 2 aaa",
        "active":true,"members":[{"userId":1,"userEmail":"sheena.oconnell@umuzi.org","permissionStudent":true,"permissionView":false,"permissionManage":false}]}
    
    }

test("cleanAndFilterUserGroups can deal with empty filter", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:""})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 1 AAA","demo group 2 aaa"]);
})

test("cleanAndFilterUserGroups can deal with whitespace filter", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:"   "})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 1 AAA","demo group 2 aaa"]);
})


test("cleanAndFilterUserGroups can deal with upper and lowecase", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:"aaa"})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 1 AAA","demo group 2 aaa"]);

})

test("cleanAndFilterUserGroups can deal with actual differences", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:"2"})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 2 aaa"]);
})

test("cleanAndFilterUserGroups can deal with multiple words", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:"demo group"})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
})

test("cleanAndFilterUserGroups can deal with multiple words in any order", () => {
    const ret = cleanAndFilterUserGroups({userGroups, filterBy:"group demo"})

    const names = ret.map((group)=>group.name)
    expect(names).toEqual(["demo group 1 AAA", "demo group 2 aaa"]);
})
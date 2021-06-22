const axios = require('axios');

async function login(){

    return await axios.post(`${BASE_URL}/api/dj-rest-auth/login/`, {
        email: TILDE_EMAIL,
        password: TILDE_PASSWORD
      })
      .then(function (response) {
        return token = (response.data.key);
      })
}


async function autoAssignReviewers(){
    const token = await login()
    axios.post(
        `${BASE_URL}/api/managment_actions/auto_assign_reviewers/`,{},
        {headers:{authorization: `Token ${token}`}}
    ).then(function(response){
        console.log(response.data)
    }).catch(function (error) {
        // handle error
        console.log("ERROR");
        console.log(error);
      })

}

autoAssignReviewers()

// curl --header "authorization: Token ${token}" --header "Content-Type: application/json" {BASE_URL}/api/

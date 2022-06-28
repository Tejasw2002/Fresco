function signUp()
{
        elements = Array.from(document.getElementsByTagName('input')).concat(Array.from(document.getElementsByTagName('select')))
	flag = true
        elements.forEach((element)=>
        {
		if(element.getAttribute('data-verified')=='false')
		{
			validate(element)
			flag = false
		} 
    })
	if (flag) document.forms[0].submit()
}

function signIn()
{
        window.location.href = '/login'
}

function emailCheck()
{
    email_element = document.getElementById("email")
    msg_element = getMessageElement(email_element)
    email = email_element.value
    msg_element.innerHTML = 'Please Wait......'
    fetch(`/sendOtp/${email}`)
		.then(function(response){
			msg_element.style.color = response.status == 200 ? 'green' : 'red'
			return response.json()
		}).then((response)=>{
			msg_element.innerHTML = response['message']
		}).catch((error)=>{
			console.log(error)
            msg_element.innerHTML = 'Please check if you have entered a valid email address'
		})
}

function otpCheck()
{
    otp_element = document.getElementById('otp')
    otp = otp_element.value
    url = "http://localhost:5000/verifyOtp"
    let headersList = 
    {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    msg_element = getMessageElement(otp_element)
    let bodyContent = JSON.stringify({"otp":otp, "email":document.getElementById('email').value});
    fetch(url, { method: "POST", body: bodyContent, headers: headersList})
        .then(function(response){
                if(response.status == 200){
                        msg_element.style.color = 'green'
                        document.getElementById("email").setAttribute('data-verified', 'true') 
                        document.getElementById("otp").setAttribute('data-verified', 'true')
                }
                else msg_element.style.color = 'red'
                return response.json();
        }).then((response)=>{
                msg_element.innerHTML = response['message']
        }).catch((error)=>{
                console.log(error)
                msg_element.innerHTML = 'Some error occured. Please try again'
        })
}

sexOptions = [{"value":"M", "label":"Male"}, {"value":"F", "label":"Female"}, {"value":"O", "label":"Other"}]
window.onload = function(){
        populate(document.getElementById("sex"), sexOptions)
}

function isEmpty(element){
    return (element.value=='') ? true : false;
}

function getMessageElement(element){
    return element.parentElement.nextElementSibling;
}

function validate(element)
{
        id = element.id
        type = element.type
        value = element.value
        error = ''
        if (!isEmpty(element))
        {
            if (id=='name')
            {
                    if (!/^[a-zA-Z ]+$/.test(value)) 
                    error = 'Only letters and spaces are allowed in this field'
            }
            else if (id=='pwd')
            {
                    if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(value)) 
                            error = 'Minimum of 8 charcaters with atleast each of the following: 1 lowercase letter, 1 uppercase letter, 1 digit and 1 special character'
            }
            else if (id=='tel')
            {
                    if (!/^\d\d\d\d\d\d\d\d\d\d$/.test(value))
                            error = 'Phone number should be of 10 digits'
                        }
                        else if(id=='cpwd')
            {
                    if(document.getElementById('pwd').value!=value)
                    error = 'Passwords do not match'
                }
            else if(id=='pin')
            {
                    if(!/^\d\d\d\d\d\d$/.test(value))
                    error = 'Pincode must be made up of 6 digits'
                }
    }
    else
            error = 'This field cannot be left blank'
    getMessageElement(element).innerHTML = error;
    if (error=='')
    {
            element.setAttribute('data-verified', true)
            element.style.borderBottomColor= 'green'
        }
    else
    {
            element.setAttribute('data-verified', false)
            element.style.borderBottomColor= 'red'
    }
}

function toggleVisibility(element)
{
    pwd = document.getElementById('pwd')
    element = element.parentElement.querySelector("i")
    if(element.classList.contains('icon-show'))
    {
            pwd.type = 'text'
            element.classList = ['icon icon-hide']
    }
    else
    {
            pwd.type = 'password'
            element.classList = ['icon icon-show']
    }
}

function populate(element, options, key="value", desc="label"){
    len = options.length
    element.innerHTML = `<option value='' selected disabled></option>`
    for (i=0; i<len; i++){
        value = options[i][key]
        label = options[i][desc]
        element.innerHTML+= `<option value=${value}>${label}</option>`
    }
}

function dismiss(element){
    element.remove();
}
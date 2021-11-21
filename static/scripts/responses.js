function getBotResponse(input) {
    return new Promise(function (resolve, reject) {
    $.ajax({
        url: "/get_answer",
        data : { question: input},
        success : function(answer) {
            $("#request-access").hide();
            console.log("requested access complete");
            console.log(answer)
            resolve(answer)
        },
        error : function() {
            reject('Sorry! Please try again');
        }
    })
})
}
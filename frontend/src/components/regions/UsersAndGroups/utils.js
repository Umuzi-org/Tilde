const timeNow = new Date()
const milliseconds = 1000 * 60 * 60 * 24
const timeDifferenceInDays = (time) => {return Math.ceil(Math.abs(timeNow - new Date(time)) / milliseconds)}
let prColor

export const getPrColor = (oldestOpenPrTime) => {
    if (timeDifferenceInDays(oldestOpenPrTime) === 1){
        prColor = "black"
    }else if(timeDifferenceInDays(oldestOpenPrTime) <= 2) {
        prColor = "orange"
    }else {
        prColor = "red"
    }
    return prColor 
}

export const getTildeReviewColor = (oldestOpenPrTime) => {
    console.log(timeDifferenceInDays(oldestOpenPrTime))
    if(timeDifferenceInDays(oldestOpenPrTime) === 1){
        prColor = "black"
    }
    else if(timeDifferenceInDays(oldestOpenPrTime) <= 3) {
        prColor = "orange"
    }else {
        prColor = "red"
    }
    return prColor 
}
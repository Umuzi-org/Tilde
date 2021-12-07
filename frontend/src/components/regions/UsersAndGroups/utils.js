export const getPrColor = ({oldestOpenPrTime}) => {
    const now = new Date()
    const milliseconds = 1000 * 60 * 60 * 24

    const timeDifferenceInSeconds = Math.abs(now - new Date(oldestOpenPrTime))
    const timeDifferenceInDays = Math.ceil(timeDifferenceInSeconds / milliseconds)

    return timeDifferenceInDays  

}
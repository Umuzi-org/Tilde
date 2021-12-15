import { cardColors } from "../../../colors";

/**
 * fillColor function returns a colour string value based on the type of column:
 * Grey for Blocked column,
 * Blue for Ready column,
 * Green for In Progress column,
 * Red for Review Feedback column,
 * Orange for Review column,
 * Yellow for Complete column
 */

export const fillColor = (columnName) => {
    if(columnName.includes('Blocked')) {
        return cardColors.B;
    }
    if(columnName.includes('Ready')) {
        return cardColors.R;
    }
    if(columnName.includes('In Progress')) {
        return cardColors.IP;
    }
    if(columnName.includes('Review Feedback')) {
        return cardColors.RF;
    }
    if(columnName.includes('Review')) {
        return cardColors.IR;
    }
    if(columnName.includes('Complete')) {
        return cardColors.C;
    }
}
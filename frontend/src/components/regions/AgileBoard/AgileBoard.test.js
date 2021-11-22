import  { boardFromCards }  from "../AgileBoard";
import { cards, latestCalls} from "./mockedData";

test("boardFromCards function returns correct total length 5 of the array", () => {
   let boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard.length).toBe(5);
});

test("boardFromCards function returns correct backlog totalCards 2 when latestCalls has 1 B and 1 R in totalCards object", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[0].totalCards).toBe(2);
});

test("boardFromCards function returns correct In Progress totalCards 1 when latestCalls has 1 IP  in totalCards object", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[1].totalCards).toBe(1);
});

test("boardFromCards function returns correct Review Feddback totalCards 0 when latestCalls has 0 RF  in totalCards object", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[2].totalCards).toBe(0);
});

test("boardFromCards function returns correct Review totalCards 0 when latestCalls has 0 R in totalCards object", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[3].totalCards).toBe(0);
});

test("boardFromCards function returns correct Complete totalCards 2 when latestCalls has 2 C in totalCards object", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[4].totalCards).toBe(2);
});
 
test("boardFromCards function returns correct label Backlog at the first index of the array", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[0].label).toBe('Backlog');
});

test("boardFromCards function returns correct label In progress at the second index of the array", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[1].label).toBe('In Progress');
});

test("boardFromCards function returns correct label Review Feedback at the third index of the array", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[2].label).toBe('Review Feedback');
});

test("boardFromCards function returns correct label Review at the fourth index of the array", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[3].label).toBe('Review');
});

test("boardFromCards function returns correct label Review at the fifth index of the array", () => {
   const boardFromCard  = boardFromCards({ cards, latestCalls });
   expect(boardFromCard[4].label).toBe('Complete');
});
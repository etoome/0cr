export interface Auth {
	username: string;
	key: string;
}

export type Leaderboard = UserScore[];

interface UserScore {
	username: string;
	score: number;
	date: Date;
}

export type Play = PlayWin | PlayLoose;

interface PlayWin {
	success: true;
	score: number;
	char: string;
}
interface PlayLoose {
	success: false;
	score: number;
}

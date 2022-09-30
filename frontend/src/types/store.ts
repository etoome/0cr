export interface User {
	username: string;
	key: string;
}

export interface Game {
	token: string;
	score: number;
	success: boolean | null;
	char?: string;
}

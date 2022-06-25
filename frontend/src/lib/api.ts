import * as store from '$lib/store';
import type { Auth, Leaderboard, Play } from 'src/types/api';
import type { Game, User } from 'src/types/store';
import { BACKEND_URL } from '$lib/variables';

export async function register(username: string): Promise<boolean> {
	const res = await fetch(`${BACKEND_URL}/register`, {
		method: 'POST',
		body: JSON.stringify({ username }),
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		}
	});
	if (!res.ok) return;
	const data = await res.json();
	if (data.username === undefined || data.key === undefined) return false;

	const auth: Auth = {
		username: data.username,
		key: data.key
	};

	store.user.set(auth);

	return true;
}

export async function login(key: string): Promise<boolean> {
	const res = await fetch(`${BACKEND_URL}/login`, {
		method: 'POST',
		body: JSON.stringify({ key }),
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		}
	});
	if (!res.ok) return;
	const data = await res.json();
	if (data.username === undefined || data.key === undefined) return false;

	const auth: Auth = {
		username: data.username,
		key: data.key
	};

	store.user.set(auth);

	return true;
}

export async function leaderboard(): Promise<Leaderboard> {
	const res = await fetch(`${BACKEND_URL}/leaderboard`, {
		method: 'GET'
	});
	if (!res.ok) return;
	const data = await res.json();
	if (data === undefined || !Array.isArray(data)) return;

	return data.map((u) => {
		if (u.username === undefined || u.score === undefined || u.date === undefined) return;
		return {
			username: u.username,
			score: u.score,
			date: new Date(u.date)
		};
	});
}

export async function newGame() {
	let user: User | null = null;
	store.user.subscribe((u) => {
		user = u;
	});

	const res = await fetch(`${BACKEND_URL}/game/new`, {
		method: 'POST',
		body: JSON.stringify({ key: user.key }),
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		}
	});
	if (!res.ok) return;
	const data = await res.json();
	if (data.token === undefined || data.char === undefined) return;

	store.game.set({ token: data.token, score: 0, success: null, char: data.char });
}

export async function play(image: string) {
	let game: Game | null = null;
	store.game.subscribe((g) => {
		game = g;
	});

	const res = await fetch(`${BACKEND_URL}/game/play`, {
		method: 'POST',
		body: JSON.stringify({ token: game.token, image }),
		headers: {
			'Content-Type': 'application/json',
			Accept: 'application/json'
		}
	});
	if (!res.ok) return;
	const data = await res.json();
	if (data.success === undefined || data.score === undefined) return;

	const play: Play = {
		success: data.success,
		score: data.score,
		char: data.char
	};

	store.game.update((g) => ({
		token: g.token,
		score: data.score,
		success: data.success,
		char: data.char
	}));

	return play;
}

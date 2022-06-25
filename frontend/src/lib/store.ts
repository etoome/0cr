import type { Game, User } from 'src/types/store';
import { writable } from 'svelte/store';

export const user = writable<User | null>(null);
export const game = writable<Game | null>(null);

export function reset() {
	user.set(null);
	game.set(null);
}

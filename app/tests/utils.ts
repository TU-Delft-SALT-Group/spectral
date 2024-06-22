import type { Page } from '@playwright/test';

type Params = { page: Page };

export const setupTests = async ({ page }: Params) => {
	await page.goto('http://localhost/admin');
	await page.getByRole('button', { name: 'Delete all data' }).click();
	await page.getByRole('button', { name: 'Seed database with sample user' }).click();
	await page.getByRole('button', { name: 'Seed database with sample session' }).click();
	await page.getByRole('button', { name: 'Seed database with TORGO' }).click();
};

export const deleteEverything = async ({ page }: Params) => {
	await page.goto('http://localhost/admin');
	await page.getByRole('button', { name: 'Delete all data' }).click();
	await page.getByRole('button', { name: 'Seed database with sample user' }).click();
	await page.getByRole('button', { name: 'Seed database with sample session' }).click();
	await page.getByRole('button', { name: 'Seed database with TORGO' }).click();
	await page.close();
};

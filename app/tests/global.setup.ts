import { test as setup } from '@playwright/test';

setup('setup the sample account', async ({ page }) => {
	await page.goto('http://localhost/admin');
	await page.getByRole('button', { name: 'Delete all data' }).click();
	await page.getByRole('button', { name: 'Seed database with sample user' }).click();
	await page.getByRole('button', { name: 'Seed database with sample session' }).click();
	await page.getByRole('button', { name: 'Seed database with TORGO' }).click();
	await page.close();
});

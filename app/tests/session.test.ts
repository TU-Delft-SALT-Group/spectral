import { test, expect } from './baseFixtures.ts';
import { deleteEverything, setupTests } from './utils.ts';

test.beforeEach(async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('S');
	await page.getByLabel('Username').press('CapsLock');
	await page.getByLabel('Username').fill('Sample');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
});

test('everything in session is visible', async ({ page }) => {
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click();
	await expect(page.locator('canvas').first()).toBeVisible();
	await expect(page.locator('canvas').nth(2)).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00.511.522.533.544.5 00:00.000/00:04.800 1.00x F01_severe_head_sentence1 00.511'
			})
			.getByRole('button')
			.first()
	).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('section')
			.filter({
				hasText: '00.511.522.533.544.5 00:00.000/00:04.800 1.00x F01_severe_head_sentence1 00.511'
			})
			.getByRole('button')
			.nth(1)
	).toBeVisible();
	await expect(page.locator('li').filter({ hasText: 'F01_severe_head_sentence1' })).toBeVisible();
	await expect(page.locator('li').filter({ hasText: 'F03_moderate_head_sentence1' })).toBeVisible();
	await expect(page.getByRole('button', { name: 'MC02_control_head_sentence1' })).toBeVisible();
	await expect(
		page.getByText('home session sample-session Spectral Show Info Profile')
	).toBeVisible();
	await expect(page.getByRole('button', { name: 'Record' })).toBeVisible();
	await expect(page.getByRole('textbox')).toBeVisible();
	await expect(page.getByText('1.00x').first()).toBeVisible();
	await expect(page.getByText('1.00x').nth(1)).toBeVisible();
});

test('session selection screen test', async ({ page }) => {
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toBeVisible();
	await expect(page.getByRole('link', { name: 'spectrum' })).toHaveCount(0);
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click({
		button: 'right'
	});
	await page.getByRole('menuitem', { name: 'Delete' }).click();
	await page.getByRole('button', { name: 'Continue' }).click();
	await expect(page.getByRole('link', { name: 'Sample Session sample-session' })).toHaveCount(0);
	await page.getByRole('button').click();
	await expect(page.getByLabel('Enter new session name')).toBeVisible();
	await page.locator('input[name="sessionName"]').click();
	await page.locator('input[name="sessionName"]').fill('spectrum');
	await page.locator('input[name="sessionName"]').press('Enter');
	await expect(page.locator('ol').filter({ hasText: 'No files yet!' })).toBeVisible();
	await page.getByRole('link', { name: 'session' }).click();
	await expect(page.getByRole('link', { name: 'spectrum' })).toBeVisible();
});

test.afterEach(deleteEverything);

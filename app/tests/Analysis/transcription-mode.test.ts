import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
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
	await page.getByRole('link', { name: 'Sample Session sample-session' }).click();
});

test('track test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(5) > .inline-flex').click();
	await expect(page.getByText('empty').first()).toBeVisible();
	await expect(page.getByRole('button', { name: 'Create New Track' }).first()).toBeVisible();
	await expect(
		page
			.getByRole('group')
			.locator('div')
			.filter({ hasText: '00.511.522.533.544.5 empty' })
			.getByRole('button')
			.nth(2)
	).toBeVisible();
	await expect(page.getByText(':00.000/00:04.800 F01_severe_head_sentence1')).toBeVisible();
	await page.getByText('empty Create New Track').nth(1).getByRole('combobox').click();
	await page.getByRole('option', { name: 'deepgram' }).click();
	await page.getByRole('button', { name: 'Create New Track' }).nth(1).click();
	await page.waitForTimeout(1000);
	await expect(page.getByText('deepgram-en', { exact: true })).toBeVisible();
	await expect(
		page.getByRole('group').locator('div').filter({ hasText: 'the quick brown fox jumps' }).nth(1)
	).toBeVisible();
	await page.getByText('deepgram Create New Track').getByRole('combobox').click();
	await page.getByRole('option', { name: 'allosaurus' }).click();
	await page.getByRole('button', { name: 'Create New Track' }).nth(1).click();
	await page.waitForTimeout(2000);
	await expect(page.getByText('allosaurus-en', { exact: true })).toBeVisible();
	await expect(
		page.getByRole('group').locator('div').filter({ hasText: 'ð æ tʰ k ʁ ɪ tʰ b̥ ɹ a w n f' }).nth(1)
	).toBeVisible();
	await page.getByText('deepgram-en', { exact: true }).click();
	await page.getByText('deepgram-en', { exact: true }).click({
		clickCount: 3
	});
	await page.getByText('deepgram-en', { exact: true }).fill('renamed');
	await expect(page.getByText('renamed', { exact: true })).toBeVisible();
	await page
		.getByRole('group')
		.locator('div')
		.filter({ hasText: 'renamed' })
		.nth(1)
		.getByRole('button')
		.nth(2)
		.click();
	await expect(page.getByText('renamed', { exact: true })).toHaveCount(0);
});

test('split test', async ({ page }) => {
	await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(5) > .inline-flex').click();
	await page.getByText('empty Create New Track').nth(1).getByRole('combobox').click();
	await page.waitForTimeout(500);
	await page.getByRole('option', { name: 'deepgram' }).click();
	await page.getByRole('button', { name: 'Create New Track' }).nth(1).click();
	await page.waitForTimeout(2000);
	await page.getByRole('button', { name: 'quick' }).click({
		modifiers: ['Shift']
	});
	await page.locator('div:nth-child(7) > .flex').dblclick();
	await page.keyboard.press('h');
	await page.keyboard.press('a');
	await page.keyboard.press('p');
	await page.keyboard.press('p');
	await page.keyboard.press('y');
	await page.keyboard.press('Enter');
	await expect(
		page.getByRole('group').locator('div').filter({ hasText: 'the quick brown fox jumps' }).nth(1)
	).toHaveCount(0);
	await expect(
		page.getByRole('group').locator('div').filter({ hasText: 'the quick happy brown fox' }).nth(1)
	).toBeVisible();
});

test.afterEach(async ({ page }) => {
	await page.close();
});

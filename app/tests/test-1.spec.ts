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

test('test', async ({ page }) => {
  await page.locator('div:nth-child(2) > .inline-flex').hover();
	await page.locator('div:nth-child(5) > .inline-flex').click();
  // await page.getByText('empty Create New Track').nth(1).getByRole('combobox').click();
  await page.getByText('empty').nth(1).click();
	await page.getByRole('option', { name: 'deepgram' }).click();
	await page.getByRole('button', { name: 'Create New Track' }).nth(1).click();
	await page.waitForTimeout(1000);
  await page.getByText('deepgram Create New Track').getByRole('combobox').click();
  await page.waitForTimeout(5000);
  await page.getByRole('option', { name: 'whisper' }).click();
  await page.getByRole('button', { name: 'Create New Track' }).nth(1).click();
	await page.waitForTimeout(1000);
  await page.getByRole('button', { name: 'brown' }).nth(1).click({
    clickCount: 3
  });
  await page.getByRole('button', { name: 'brown' }).nth(1).fill('red');
  await page.getByRole('button', { name: 'fox' }).nth(1).click({
    clickCount: 3
  });
  await page.getByRole('button', { name: 'fox' }).nth(1).fill('box');
  await page.getByRole('button', { name: 'jumps' }).nth(1).click({
    clickCount: 3
  });
  await page.getByRole('button', { name: 'jumps' }).nth(1).fill('junks');
  await page.getByRole('button', { name: 'lazy' }).nth(1).click({
    clickCount: 3
  });
  await page.getByRole('button', { name: 'lazy' }).nth(1).fill('lady');
  await page.locator('div:nth-child(5) > .inline-flex').hover();
  await page.locator('div:nth-child(6) > .inline-flex').click();
  await expect(page.getByRole('heading', { name: 'F03_moderate_head_sentence1' })).toBeVisible();
  await expect(page.getByText('Reference track').nth(1)).toBeVisible();
  await expect(page.getByText('Hypothesis track').nth(1)).toBeVisible();
  await page.getByRole('combobox').nth(2).click();
  await page.getByRole('option', { name: 'deepgram-en' }).click();
  await page.getByRole('combobox').nth(3).click();
  await page.getByRole('option', { name: 'whisper-english' }).click();
});
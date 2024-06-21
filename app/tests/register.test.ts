import { test, expect } from './baseFixtures.ts';
import { deleteEverything, setupTests } from './utils.ts';

test.use({
	viewport: {
		height: 850,
		width: 1600
	}
});

test('register and walk through', async ({ page }) => {
	await setupTests({ page });
	await page.goto('http://localhost/');
	await page.getByRole('link', { name: 'Analyze' }).click();
	await page.getByRole('link', { name: 'Sign up instead' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Roman');
	await page.getByLabel('Email').click();
	await page.getByLabel('Email').fill('fake');
	await page.getByLabel('Password').click();
	await expect(page.locator('form')).toContainText('Invalid email');
	await page.getByLabel('Email').click();
	await page.getByLabel('Email').fill('fake@fake.gmail');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('pass');
	await page.locator('div').filter({ hasText: 'Sign up Username Email' }).nth(1).click();
	await expect(page.getByText('String must contain at least')).toBeVisible();
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await expect(page.getByRole('button')).toBeVisible();
	await page.waitForTimeout(100);
	await page.getByRole('button').click();
	await page.waitForTimeout(100);
	await expect(page.locator('div').filter({ hasText: 'Profile' }).nth(2)).toBeVisible();
	await page.locator('input[name="sessionName"]').click();
	await page.locator('input[name="sessionName"]').fill('new session asdf');
	await page.locator('input[name="sessionName"]').press('Enter');
	await expect(page.getByRole('main').filter({ hasNotText: 'sessions' })).toContainText(
		'No files yet!'
	);
	await expect(page.getByRole('main')).toContainText('Record');
	await page.getByRole('link', { name: 'session' }).click();
	await expect(page.locator('h2')).toContainText('new session asdf');
	await page.getByRole('link', { name: 'Profile' }).click();
	await expect(page.getByRole('strong')).toContainText('Roman');
	await expect(page.locator('body')).toContainText(
		'You have uploaded 0 files and have 1 sessions.'
	);
	await page.getByRole('button', { name: 'Log out' }).click();
	await page.getByLabel('Username').click();
	await page.getByLabel('Username').fill('Roman');
	await page.getByLabel('Password').click();
	await page.getByLabel('Password').fill('password');
	await page.getByRole('button', { name: 'Submit' }).click();
	await expect(page.locator('h2')).toContainText('new session asdf');
});

test.afterEach(deleteEverything);

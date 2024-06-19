import { PlaywrightTestConfig, devices } from '@playwright/test';

const config: PlaywrightTestConfig = {
	webServer: {
		command: 'docker compose up --build',
		url: 'http://localhost:80',
		timeout: 600 * 1000,
		reuseExistingServer: !process.env.CI
	},
	projects: [
		{
			name: 'setup sample account',
			testMatch: /global\.setup\.ts/,
			teardown: 'cleanup db and preserve sample account'
		},
		{
			name: 'cleanup db and preserve sample account',
			testMatch: /global\.teardown\.ts/
		},
		{
			name: 'firefox',
			use: { ...devices['Desktop Firefox'] },
			dependencies: ['setup sample account']
		},
		{
			name: 'chromium',
			use: { ...devices['Desktop Chrome'], permissions: ['microphone', 'camera'] },
			dependencies: ['setup sample account']
		}
	],
	use: {
		baseURL: 'http://localhost:80',
		actionTimeout: 10000,
		navigationTimeout: 10000
	},
	expect: {
		timeout: 10000
	},
	testDir: 'tests',
	testMatch: /(.+\.)?(test|spec)\.[jt]s/
};

export default config;

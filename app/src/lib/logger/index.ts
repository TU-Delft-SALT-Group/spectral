const pino = await import('pino');

export const logger = pino.pino({
	transport: {
		target: 'pino-pretty',
		options: {
			colorize: true
		}
	}
});

# Payments and Tax Presentation Policy

## Current public position

Tender Getter RSA is currently configured as:

```text
tax_mode: not_registered
```

Customer-visible catalogue amounts are the final amounts charged. Until Tender Getter is VAT registered, customer messages and invoices must state:

> Tender Getter RSA is not currently VAT registered. No VAT is charged.

Do not use “VAT inclusive”, “VAT exclusive”, “plus VAT”, or display a VAT line while this configuration is active.

## Future tax configuration

The database owns tax presentation through `billing_tax_configuration`:

```text
not_registered  → displayed catalogue price is final; tax is R0
vat_inclusive   → displayed catalogue price is final; VAT is included in it
vat_exclusive   → catalogue price is subtotal; VAT is added at checkout
```

Only an authorised business decision after VAT registration may change the configuration. This is not a runtime environment variable and must not be guessed by the AI agent.

## Bank-neutral customer language

Never market Tender Getter as tied to a specific bank. Use:

> Pay securely by card, secure bank payment, or debit order, depending on the options available to you.

Never say “all banks are supported”. The provider-hosted checkout must display only payment methods that are actually available to that customer.

Debit-order and DebiCheck messages must say that the customer will approve a provider-hosted mandate through their banking channel. Tender Getter never collects banking details, PINs, passwords, OTPs or mandate information in WhatsApp.

## Annual payment

Annual pricing is an upfront annual checkout. The annual saving applies only when the full annual amount is paid upfront. Monthly debit order remains a monthly collection and uses monthly pricing.

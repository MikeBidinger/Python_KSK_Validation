# Python_KSK_Validation

This will project minimize failures and maximize seamless production within our plant by continues order validations for all sales order (configuration check).

By validating every sales order against the defined and agreed KSK (Kundenspezifischer Kabelbaum, this translates to custom wiring harness) documentation. To guaranty 100% quality (for the wiring harness configuration) all the sales orders have to passthrough a series of validations. Every day, every sales order will be validated, and when a sales order fails at least one of these validations, it will be marked as an incorrect configured order (done by a follow-up application) and these will be unable to be planned. This will guaranty seamless production.

In a nutshell the validations exists out of:
-	Missing step validation
-	Multiple step validation
-	BOM (= Bill Of Material) vs documentation validation

<i> * This project includes hashing (###) for sensitive data/info.</i>

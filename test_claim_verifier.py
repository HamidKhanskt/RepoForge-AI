from src.evaluation.claim_verifier import verify_claims


good_claim = """
The checkout function calls get_product() for each product.
The repository contains calculate_shipping().
"""


bad_claim = """
The checkout endpoint uses Flask Blueprint and request.form.
The database uses cursor.execute with SELECT *.
"""


print("\n" + "=" * 70)
print("              CLAIM VERIFIER")
print("=" * 70)

print("\nGOOD CLAIM")
print("-" * 70)
print(verify_claims(good_claim))

print("\nBAD CLAIM")
print("-" * 70)
print(verify_claims(bad_claim))

print("\n" + "=" * 70)

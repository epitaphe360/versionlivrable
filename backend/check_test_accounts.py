"""Vérifier les comptes de test dans Supabase"""
from supabase_client import supabase

print("=== VÉRIFICATION DES COMPTES DE TEST ===\n")

# 1. Admin
print("1. ADMIN:")
admin = supabase.table("users").select("*").eq("email", "admin@getyourshare.com").execute()
print(f"   admin@getyourshare.com: {'✅ EXISTE' if admin.data else '❌ N\'EXISTE PAS'}")
if admin.data:
    print(f"   Role: {admin.data[0].get('role')}, Tier: {admin.data[0].get('tier')}")

# 2. Influenceurs
print("\n2. INFLUENCEURS:")
influencers = [
    ("Hassan Oudrhiri", "hassan.oudrhiri@getyourshare.com", "STARTER"),
    ("Sarah Benali", "sarah.benali@getyourshare.com", "PRO"),
    ("Karim Benjelloun", "karim.benjelloun@getyourshare.com", "ENTERPRISE")
]

for name, email, tier in influencers:
    user = supabase.table("users").select("*").eq("email", email).execute()
    print(f"   {name} ({email}):")
    print(f"      {'✅ EXISTE' if user.data else '❌ N\'EXISTE PAS'}")
    if user.data:
        print(f"      Role: {user.data[0].get('role')}, Tier: {user.data[0].get('tier')}")

# 3. Marchands
print("\n3. MARCHANDS:")
merchants = [
    ("Boutique Maroc", "boutique.maroc@getyourshare.com", "STARTER"),
    ("Luxury Crafts", "luxury.crafts@getyourshare.com", "PRO"),
    ("ElectroMaroc", "electro.maroc@getyourshare.com", "ENTERPRISE")
]

for name, email, tier in merchants:
    user = supabase.table("users").select("*").eq("email", email).execute()
    print(f"   {name} ({email}):")
    print(f"      {'✅ EXISTE' if user.data else '❌ N\'EXISTE PAS'}")
    if user.data:
        print(f"      Role: {user.data[0].get('role')}, Tier: {user.data[0].get('tier')}")

# 4. Commercial
print("\n4. COMMERCIAL:")
commercial = supabase.table("users").select("*").eq("email", "sofia.chakir@getyourshare.com").execute()
print(f"   Sofia Chakir (sofia.chakir@getyourshare.com):")
print(f"      {'✅ EXISTE' if commercial.data else '❌ N\'EXISTE PAS'}")
if commercial.data:
    print(f"      Role: {commercial.data[0].get('role')}, Tier: {commercial.data[0].get('tier')}")

# Vérifier TOUS les utilisateurs
print("\n\n=== TOUS LES UTILISATEURS DANS LA BASE ===")
all_users = supabase.table("users").select("*").execute()
print(f"Total utilisateurs: {len(all_users.data)}\n")

if all_users.data:
    # Afficher les colonnes disponibles
    print("Colonnes disponibles:", list(all_users.data[0].keys()))
    print()
    
    for user in all_users.data[:15]:  # Afficher les 15 premiers
        email = user.get('email', 'N/A')
        role = user.get('role', 'N/A')
        subscription = user.get('subscription_tier', 'N/A')
        company = user.get('company_name', 'N/A')
        print(f"   - {email:40} | {role:12} | {subscription:12} | {company}")
else:
    print("❌ AUCUN utilisateur dans la base de données !")

import { Platform } from "react-native";
import Purchases, {
  CustomerInfo,
  PurchasesPackage,
} from "react-native-purchases";

const SUPPORTER_ENTITLEMENT = "supporter";

let configured = false;

function platformKey(): string | undefined {
  if (Platform.OS === "ios") {
    return process.env.EXPO_PUBLIC_REVENUECAT_IOS_KEY;
  }
  if (Platform.OS === "android") {
    return process.env.EXPO_PUBLIC_REVENUECAT_ANDROID_KEY;
  }
  return undefined;
}

export async function configureRevenueCat(): Promise<boolean> {
  if (configured) return true;
  const apiKey = platformKey();
  if (!apiKey) return false;

  Purchases.configure({ apiKey });
  configured = true;
  return true;
}

export function isRevenueCatConfigured(): boolean {
  return configured;
}

export function hasSupporterEntitlement(info: CustomerInfo): boolean {
  return Boolean(info.entitlements.active[SUPPORTER_ENTITLEMENT]);
}

export async function readSupporterState(): Promise<boolean> {
  if (!configured) return false;
  const info = await Purchases.getCustomerInfo();
  return hasSupporterEntitlement(info);
}

export async function currentSupporterPackage(): Promise<PurchasesPackage | null> {
  if (!configured) return null;
  const offerings = await Purchases.getOfferings();
  const current = offerings.current;
  if (!current || current.availablePackages.length === 0) return null;
  return current.availablePackages[0];
}

export async function purchaseSupporterTheme(
  pack: PurchasesPackage
): Promise<boolean> {
  if (!configured) return false;
  const result = await Purchases.purchasePackage(pack);
  return hasSupporterEntitlement(result.customerInfo);
}

export async function restoreSupporterTheme(): Promise<boolean> {
  if (!configured) return false;
  const info = await Purchases.restorePurchases();
  return hasSupporterEntitlement(info);
}

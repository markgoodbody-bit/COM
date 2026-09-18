import React, { useEffect, useMemo, useState } from "react";
import {
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  Share,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import {
  configureRevenueCat,
  currentSupporterPackage,
  purchaseSupporterTheme,
  readSupporterState,
  restoreSupporterTheme,
} from "./src/revenuecat";

type Draft = {
  happening: string;
  observed: string;
  reported: string;
  inferred: string;
  unknown: string;
  matters: string;
  reachable: string;
  hardening: string;
  next: string;
};

type Step =
  | "start"
  | "happening"
  | "know"
  | "matters"
  | "reachable"
  | "time"
  | "next"
  | "summary";

const EMPTY_DRAFT: Draft = {
  happening: "",
  observed: "",
  reported: "",
  inferred: "",
  unknown: "",
  matters: "",
  reachable: "",
  hardening: "",
  next: "",
};

const STEP_ORDER: Step[] = [
  "start",
  "happening",
  "know",
  "matters",
  "reachable",
  "time",
  "next",
  "summary",
];

const CORE_STEPS = STEP_ORDER.length - 2;

function clean(value: string): string {
  return value.trim();
}

function summaryText(draft: Draft): string {
  const parts = [
    ["What is happening", draft.happening],
    ["Observed", draft.observed],
    ["Reported", draft.reported],
    ["Inferred", draft.inferred],
    ["Unknown", draft.unknown],
    ["What matters now", draft.matters],
    ["What is reachable", draft.reachable],
    ["What changes with time", draft.hardening],
    ["One next move", draft.next],
  ]
    .filter(([, value]) => clean(value))
    .map(([label, value]) => `${label}\n${clean(value)}`);

  return [
    "PLEASE START FROM HERE",
    "",
    ...parts,
    "",
    "This note is a snapshot, not a score or diagnosis.",
  ].join("\n");
}

function Field({
  label,
  value,
  onChangeText,
  placeholder,
  minHeight = 120,
}: {
  label?: string;
  value: string;
  onChangeText: (value: string) => void;
  placeholder: string;
  minHeight?: number;
}) {
  return (
    <View style={styles.fieldWrap}>
      {label ? <Text style={styles.fieldLabel}>{label}</Text> : null}
      <TextInput
        multiline
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor="#77736a"
        textAlignVertical="top"
        style={[styles.input, { minHeight }]}
      />
    </View>
  );
}

function Button({
  title,
  onPress,
  quiet = false,
  disabled = false,
}: {
  title: string;
  onPress: () => void;
  quiet?: boolean;
  disabled?: boolean;
}) {
  return (
    <Pressable
      accessibilityRole="button"
      disabled={disabled}
      onPress={onPress}
      style={({ pressed }) => [
        styles.button,
        quiet && styles.buttonQuiet,
        disabled && styles.buttonDisabled,
        pressed && !disabled && styles.buttonPressed,
      ]}
    >
      <Text
        style={[
          styles.buttonText,
          quiet && styles.buttonQuietText,
          disabled && styles.buttonDisabledText,
        ]}
      >
        {title}
      </Text>
    </Pressable>
  );
}

export default function App() {
  const [draft, setDraft] = useState<Draft>(EMPTY_DRAFT);
  const [stepIndex, setStepIndex] = useState(0);
  const [supporter, setSupporter] = useState(false);
  const [supportReady, setSupportReady] = useState(false);
  const [supportBusy, setSupportBusy] = useState(false);

  const step = STEP_ORDER[stepIndex];
  const palette = supporter ? supporterPalette : basePalette;

  useEffect(() => {
    let active = true;

    (async () => {
      try {
        const ok = await configureRevenueCat();
        if (!active || !ok) return;
        const entitled = await readSupporterState();
        if (!active) return;
        setSupporter(entitled);
        setSupportReady(true);
      } catch {
        if (active) setSupportReady(false);
      }
    })();

    return () => {
      active = false;
    };
  }, []);

  const progress = useMemo(() => {
    if (step === "start") return 0;
    if (step === "summary") return 1;
    return Math.min(1, stepIndex / CORE_STEPS);
  }, [step, stepIndex]);

  function patch(key: keyof Draft, value: string) {
    setDraft((current) => ({ ...current, [key]: value }));
  }

  function next() {
    setStepIndex((current) => Math.min(STEP_ORDER.length - 1, current + 1));
  }

  function back() {
    setStepIndex((current) => Math.max(0, current - 1));
  }

  function reset() {
    Alert.alert(
      "Forget this note?",
      "This spike keeps the note only in app memory. This clears it now.",
      [
        { text: "Keep it", style: "cancel" },
        {
          text: "Forget it",
          style: "destructive",
          onPress: () => {
            setDraft(EMPTY_DRAFT);
            setStepIndex(0);
          },
        },
      ]
    );
  }

  async function shareSummary() {
    await Share.share({ message: summaryText(draft) });
  }

  async function buySupport() {
    setSupportBusy(true);
    try {
      const pack = await currentSupporterPackage();
      if (!pack) {
        Alert.alert(
          "No supporter product configured",
          "The purchase seam is wired, but this spike has no store product or RevenueCat offering."
        );
        return;
      }
      const unlocked = await purchaseSupporterTheme(pack);
      setSupporter(unlocked);
    } catch (error) {
      Alert.alert("Purchase not completed", String(error));
    } finally {
      setSupportBusy(false);
    }
  }

  async function restoreSupport() {
    setSupportBusy(true);
    try {
      const unlocked = await restoreSupporterTheme();
      setSupporter(unlocked);
      if (!unlocked) {
        Alert.alert("Nothing to restore", "No active supporter entitlement was found.");
      }
    } catch (error) {
      Alert.alert("Restore failed", String(error));
    } finally {
      setSupportBusy(false);
    }
  }

  return (
    <SafeAreaView style={[styles.safe, { backgroundColor: palette.background }]}>
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : undefined}
        style={styles.flex}
      >
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.brandRow}>
            <Text style={[styles.brand, { color: palette.muted }]}>PSFH</Text>
            {step !== "start" ? (
              <Pressable onPress={reset}>
                <Text style={[styles.forget, { color: palette.muted }]}>forget</Text>
              </Pressable>
            ) : null}
          </View>

          {step !== "start" ? (
            <View style={styles.progressTrack}>
              <View
                style={[
                  styles.progressFill,
                  {
                    width: `${Math.round(progress * 100)}%`,
                    backgroundColor: palette.accent,
                  },
                ]}
              />
            </View>
          ) : null}

          <View
            style={[
              styles.card,
              {
                backgroundColor: palette.card,
                borderColor: palette.border,
              },
            ]}
          >
            {step === "start" ? (
              <>
                <Text style={[styles.eyebrow, { color: palette.accent }]}>
                  PLEASE START FROM HERE
                </Text>
                <Text style={[styles.hero, { color: palette.text }]}>
                  You do not need a plan before you begin.
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  This is a small private place to sort out what is happening,
                  what you actually know, what matters now, and one move that is
                  still reachable.
                </Text>
                <Text style={[styles.note, { color: palette.muted }]}>
                  No score. No diagnosis. No account. In this spike, your note is
                  not uploaded anywhere.
                </Text>
                <Button title="Start" onPress={next} />
              </>
            ) : null}

            {step === "happening" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  1 · LOOK
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What is happening?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  Not the whole story. Just enough to name the situation you are
                  in.
                </Text>
                <Field
                  value={draft.happening}
                  onChangeText={(value) => patch("happening", value)}
                  placeholder="A few sentences is enough."
                />
              </>
            ) : null}

            {step === "know" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  2 · SEPARATE
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What do you actually know?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  Keep different kinds of knowledge separate. Empty is allowed.
                </Text>
                <Field
                  label="Observed"
                  value={draft.observed}
                  onChangeText={(value) => patch("observed", value)}
                  placeholder="What did you directly see, hear, receive, measure or experience?"
                  minHeight={86}
                />
                <Field
                  label="Reported"
                  value={draft.reported}
                  onChangeText={(value) => patch("reported", value)}
                  placeholder="What has someone or some source told you?"
                  minHeight={86}
                />
                <Field
                  label="Inferred"
                  value={draft.inferred}
                  onChangeText={(value) => patch("inferred", value)}
                  placeholder="What are you concluding from the evidence?"
                  minHeight={86}
                />
                <Field
                  label="Unknown"
                  value={draft.unknown}
                  onChangeText={(value) => patch("unknown", value)}
                  placeholder="What is still missing, ambiguous or genuinely unknown?"
                  minHeight={86}
                />
              </>
            ) : null}

            {step === "matters" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  3 · ORIENT
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What matters now?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  People, obligations, safety, time, dignity, money, trust,
                  something else. Name what is load-bearing here.
                </Text>
                <Field
                  value={draft.matters}
                  onChangeText={(value) => patch("matters", value)}
                  placeholder="What would you regret overlooking?"
                />
              </>
            ) : null}

            {step === "reachable" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  4 · FIND A ROUTE
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What is actually reachable?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  Not the perfect solution. Which actions, people, tools or
                  routes are genuinely available from where you are?
                </Text>
                <Field
                  value={draft.reachable}
                  onChangeText={(value) => patch("reachable", value)}
                  placeholder="Things I could really do, ask, check, stop, preserve or try..."
                />
              </>
            ) : null}

            {step === "time" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  5 · NOTICE TIME
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What changes if you wait?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  Some things stay correctable. Others harden, expire or become
                  much more expensive to repair.
                </Text>
                <Field
                  value={draft.hardening}
                  onChangeText={(value) => patch("hardening", value)}
                  placeholder="Deadlines, worsening conditions, disappearing evidence, commitments..."
                />
              </>
            ) : null}

            {step === "next" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  6 · ACT SMALL
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  What is one next move?
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  Choose something small enough to do, meaningful enough to
                  matter, and correctable if you learn something new.
                </Text>
                <Field
                  value={draft.next}
                  onChangeText={(value) => patch("next", value)}
                  placeholder="One thing I can do next is..."
                />
              </>
            ) : null}

            {step === "summary" ? (
              <>
                <Text style={[styles.stepLabel, { color: palette.accent }]}>
                  WHERE YOU ARE
                </Text>
                <Text style={[styles.title, { color: palette.text }]}>
                  A usable snapshot.
                </Text>
                <Text style={[styles.body, { color: palette.body }]}>
                  This is not a verdict. It is a place to look from.
                </Text>

                <View
                  style={[
                    styles.summary,
                    {
                      backgroundColor: palette.summary,
                      borderColor: palette.border,
                    },
                  ]}
                >
                  {[
                    ["Happening", draft.happening],
                    ["Observed", draft.observed],
                    ["Reported", draft.reported],
                    ["Inferred", draft.inferred],
                    ["Unknown", draft.unknown],
                    ["Matters now", draft.matters],
                    ["Reachable", draft.reachable],
                    ["Time changes", draft.hardening],
                    ["Next move", draft.next],
                  ]
                    .filter(([, value]) => clean(value))
                    .map(([label, value]) => (
                      <View key={label} style={styles.summaryBlock}>
                        <Text style={[styles.summaryLabel, { color: palette.accent }]}>
                          {label}
                        </Text>
                        <Text style={[styles.summaryText, { color: palette.text }]}>
                          {clean(value)}
                        </Text>
                      </View>
                    ))}
                </View>

                <Button title="Share this snapshot" onPress={shareSummary} />
                <Button
                  title="Go through it again"
                  onPress={() => setStepIndex(1)}
                  quiet
                />

                <View style={[styles.supportBox, { borderColor: palette.border }]}>
                  <Text style={[styles.supportTitle, { color: palette.text }]}>
                    Keep the gift free.
                  </Text>
                  <Text style={[styles.note, { color: palette.muted }]}>
                    The competition requires RevenueCat. The proposed paid item is
                    deliberately cosmetic: a supporter theme. Nothing in the core
                    flow is locked.
                  </Text>

                  {supportReady ? (
                    <>
                      <Button
                        title={
                          supporter
                            ? "Supporter theme active"
                            : supportBusy
                              ? "Checking…"
                              : "Unlock supporter theme"
                        }
                        onPress={buySupport}
                        disabled={supporter || supportBusy}
                      />
                      <Button
                        title="Restore purchase"
                        onPress={restoreSupport}
                        quiet
                        disabled={supportBusy}
                      />
                    </>
                  ) : (
                    <Text style={[styles.notConfigured, { color: palette.muted }]}>
                      RevenueCat is not configured in this spike.
                    </Text>
                  )}
                </View>
              </>
            ) : null}
          </View>

          {step !== "start" && step !== "summary" ? (
            <View style={styles.navRow}>
              <Button title="Back" onPress={back} quiet />
              <View style={styles.navSpacer} />
              <Button title="Continue" onPress={next} />
            </View>
          ) : null}

          <Text style={[styles.footer, { color: palette.muted }]}>
            Private by default · correctable by design · no universal score
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const basePalette = {
  background: "#12110f",
  card: "#1b1916",
  summary: "#151411",
  border: "#34302a",
  text: "#f0eadf",
  body: "#c9c0b2",
  muted: "#8e877b",
  accent: "#dc9b58",
};

const supporterPalette = {
  background: "#1a1612",
  card: "#251f19",
  summary: "#18130f",
  border: "#5b4630",
  text: "#fff1df",
  body: "#dbc9b5",
  muted: "#a8937a",
  accent: "#f0b86f",
};

const styles = StyleSheet.create({
  flex: { flex: 1 },
  safe: { flex: 1 },
  scroll: {
    flexGrow: 1,
    paddingHorizontal: 20,
    paddingTop: 14,
    paddingBottom: 32,
  },
  brandRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    minHeight: 34,
  },
  brand: {
    fontSize: 12,
    letterSpacing: 3,
    fontWeight: "700",
  },
  forget: {
    fontSize: 13,
  },
  progressTrack: {
    height: 2,
    marginTop: 10,
    marginBottom: 18,
    backgroundColor: "#28241f",
    overflow: "hidden",
    borderRadius: 2,
  },
  progressFill: {
    height: 2,
  },
  card: {
    borderWidth: 1,
    borderRadius: 22,
    paddingHorizontal: 20,
    paddingVertical: 24,
  },
  eyebrow: {
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 2.4,
    marginBottom: 18,
  },
  hero: {
    fontSize: 36,
    lineHeight: 42,
    fontWeight: "600",
    letterSpacing: -0.8,
    marginBottom: 18,
  },
  stepLabel: {
    fontSize: 12,
    fontWeight: "800",
    letterSpacing: 2,
    marginBottom: 12,
  },
  title: {
    fontSize: 30,
    lineHeight: 36,
    fontWeight: "600",
    letterSpacing: -0.5,
    marginBottom: 12,
  },
  body: {
    fontSize: 17,
    lineHeight: 25,
    marginBottom: 18,
  },
  note: {
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 18,
  },
  fieldWrap: {
    marginBottom: 14,
  },
  fieldLabel: {
    color: "#a9a195",
    fontSize: 13,
    fontWeight: "700",
    marginBottom: 7,
  },
  input: {
    backgroundColor: "#0f0e0c",
    borderColor: "#34302a",
    borderWidth: 1,
    borderRadius: 14,
    color: "#f4eee4",
    fontSize: 16,
    lineHeight: 23,
    padding: 14,
  },
  button: {
    minHeight: 50,
    borderRadius: 14,
    backgroundColor: "#eee5d6",
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 18,
    marginTop: 10,
  },
  buttonQuiet: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "#454038",
  },
  buttonDisabled: {
    opacity: 0.45,
  },
  buttonPressed: {
    opacity: 0.82,
  },
  buttonText: {
    color: "#171411",
    fontSize: 16,
    fontWeight: "700",
  },
  buttonQuietText: {
    color: "#c9c0b2",
  },
  buttonDisabledText: {
    color: "#8e877b",
  },
  navRow: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 10,
  },
  navSpacer: {
    flex: 1,
    minWidth: 12,
  },
  summary: {
    borderWidth: 1,
    borderRadius: 16,
    padding: 16,
    marginVertical: 8,
  },
  summaryBlock: {
    marginBottom: 16,
  },
  summaryLabel: {
    fontSize: 11,
    fontWeight: "800",
    letterSpacing: 1.3,
    textTransform: "uppercase",
    marginBottom: 5,
  },
  summaryText: {
    fontSize: 16,
    lineHeight: 23,
  },
  supportBox: {
    borderTopWidth: 1,
    marginTop: 26,
    paddingTop: 22,
  },
  supportTitle: {
    fontSize: 20,
    fontWeight: "600",
    marginBottom: 8,
  },
  notConfigured: {
    fontSize: 13,
    marginTop: 4,
  },
  footer: {
    textAlign: "center",
    fontSize: 12,
    marginTop: 22,
    paddingHorizontal: 16,
  },
});

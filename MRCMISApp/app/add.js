import { View, Text, StyleSheet, Button, TextInput } from "react-native";
import { useState } from "react";
import { useRouter } from "expo-router";

export default function AddHousehold() {
  const [householdName, setHouseholdName] = useState("");
  const router = useRouter();

  const saveHousehold = () => {
    console.log("Household saved:", householdName);
    router.back(); // Go back to home
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>➕ Add Household</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter household name"
        value={householdName}
        onChangeText={setHouseholdName}
      />
      <Button title="Save" onPress={saveHousehold} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#FFF",
  },
  title: {
    fontSize: 22,
    fontWeight: "bold",
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#CCC",
    padding: 10,
    marginBottom: 20,
    borderRadius: 5,
  },
});

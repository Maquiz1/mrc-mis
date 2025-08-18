import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet } from 'react-native';
import axios from 'axios';

export default function HouseholdForm({ navigation, route }) {
  const household = route.params?.household;
  const [name, setName] = useState(household?.name || '');
  const [expected, setExpected] = useState(household?.expected_households?.toString() || '');
  const [reached, setReached] = useState(household?.reached_households?.toString() || '');
  const [nets, setNets] = useState(household?.nets_required?.toString() || '');

  const saveData = async () => {
    try {
      if (household) {
        await axios.put(`http://192.168.100.108/api/households/${household.id}/`, {
          name, expected_households: expected, reached_households: reached, nets_required: nets
        });
      } else {
        await axios.post(`http://192.168.100.108/api/households/`, {
          name, expected_households: expected, reached_households: reached, nets_required: nets
        });
      }
      navigation.goBack();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <View style={styles.container}>
      <Text>Name:</Text>
      <TextInput style={styles.input} value={name} onChangeText={setName} />
      <Text>Expected Households:</Text>
      <TextInput style={styles.input} value={expected} onChangeText={setExpected} keyboardType="numeric" />
      <Text>Reached Households:</Text>
      <TextInput style={styles.input} value={reached} onChangeText={setReached} keyboardType="numeric" />
      <Text>Nets Required:</Text>
      <TextInput style={styles.input} value={nets} onChangeText={setNets} keyboardType="numeric" />
      <Button title="Save" onPress={saveData} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 10 },
  input: { borderWidth: 1, padding: 8, marginVertical: 5, borderRadius: 5 }
});

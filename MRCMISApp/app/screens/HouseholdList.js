import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import axios from 'axios';

export default function HouseholdList({ navigation }) {
  const [households, setHouseholds] = useState([]);

  const fetchData = async () => {
    try {
      const res = await axios.get('http://192.168.100.108/api/households/');
      setHouseholds(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', fetchData);
    return unsubscribe;
  }, [navigation]);

  return (
    <View style={styles.container}>
      <Button title="Add Household" onPress={() => navigation.navigate('Add Household')} />
      <FlatList
        data={households}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity onPress={() => navigation.navigate('Edit Household', { household: item })}>
            <View style={styles.item}>
              <Text style={styles.title}>{item.name}</Text>
              <Text>Expected: {item.expected_households}</Text>
              <Text>Reached: {item.reached_households}</Text>
              <Text>Nets Required: {item.nets_required}</Text>
            </View>
          </TouchableOpacity>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 10 },
  item: { padding: 15, backgroundColor: '#f9f9f9', marginVertical: 5, borderRadius: 5 },
  title: { fontSize: 18, fontWeight: 'bold' },
});

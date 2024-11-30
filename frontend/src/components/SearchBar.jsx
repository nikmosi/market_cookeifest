import React from "react";
import styles from "./SearchBar.module.css";
import { Link } from "react-router-dom";

export const SearchBar = () => {
	return (
		<form
			className={styles.searchContainer}
			onSubmit={(e) => e.preventDefault()}
		>
			<label htmlFor="searchInput" className={styles.visuallyHidden}>
				введите ссылку
			</label>
			<input
				id="searchInput"
				type="text"
				className={styles.searchInput}
				placeholder="введите ссылку"
			/>
			<Link to="/resault">
				<button type="submit" className={styles.searchButton}>
					найти
				</button>
			</Link>
		</form>
	);
};

// export default function BookingsList({ onComponentSelect }) {
// 	return (
// 		<div className={styles.bookingsColumn}>
// 			<nav className={styles.bookingsList}>
// 				<Link onClick={() => onComponentSelect(<UserInfo />)}>
// 					<h2 className={styles.sectionTitle}>Данные</h2>
// 				</Link>
// 				<Link onClick={() => onComponentSelect(<DoneBooking />)}>
// 					<div className={styles.activeBookings}>Завершённые брони</div>
// 				</Link>
// 				<Link onClick={() => onComponentSelect(<ActivBooking />)}>
// 					<div className={styles.activeBookings}>Активные брони</div>
// 				</Link>
// 				<div className={styles.activeBookings}>Турниры</div>
// 			</nav>
// 		</div>
// 	);
// }

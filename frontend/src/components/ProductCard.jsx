import React from 'react';
import styles from './ProductCard.module.css';

export const ProductCard = ({ title, description, price, deliveryDate }) => {
  return (
    <article className={styles.productCard}>
      <div className={styles.imageContainer} />
      <h2 className={styles.productTitle}>{title}</h2>
      <p className={styles.productDescription}>{description}</p>
      <div className={styles.productDetails}>
        <p className={styles.priceDelivery}>
          цена: {price}
          <br />
          <br />
          доставят: {deliveryDate}
        </p>
        <button className={styles.actionButton}>перейти</button>
      </div>
    </article>
  );
};
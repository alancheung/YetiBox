import styles from './Home.module.scss';
import type { ReactElement } from 'react';

import logo from '../../assets/logo.png'

function HomeComponent(): ReactElement {
    return (
        <div className={'text-center ' + styles.body}>
            <img className={styles.logo} src={logo}></img>
            <h1>
                YetiBox Control Station
            </h1>
            <table className='table w-auto mx-auto'>
                <thead>
                    <tr>
                        <td scope='col'>Thread Status</td>
                        <td scope='col'>Camera Name</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>???</td>
                        <td>???</td>
                    </tr>
                    <tr>
                        <td>???</td>
                        <td>???</td>
                    </tr>
                    <tr>
                        <td>???</td>
                        <td>???</td>
                    </tr>
                    <tr>
                        <td>???</td>
                        <td>???</td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
}

export default HomeComponent
